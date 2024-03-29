FROM gradescope/auto-builds:ubuntu-20.04

ARG s3_prv_key
ARG s3_pub_key
ARG hw
ENV hw=$hw

RUN set -eux; \
	apt update; \
	apt install -y --no-install-recommends software-properties-common; \
	apt update; \
	add-apt-repository -y ppa:ubuntu-toolchain-r/test; \
	add-apt-repository ppa:linuxuprising/java -y; \
    add-apt-repository ppa:deadsnakes/ppa -y; \
	apt-get update;

RUN set -eux; \
	echo oracle-java11-installer shared/accepted-oracle-license-v1-3 select true | /usr/bin/debconf-set-selections && \
	apt-get install -y --no-install-recommends \
		g++-11 \
		oracle-java17-installer \
		oracle-java17-set-default \
		git \
		cmake \
		curl \
		pkg-config \
		uuid-dev \
		make \
        python3;
	# update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110 --slave /usr/bin/g++ g++ /usr/bin/g++-11 --slave /usr/bin/gcov gcov /usr/bin/gcov-11 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-11 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-11  --slave /usr/bin/cpp cpp /usr/bin/cpp-11

RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
  && curl -fsSL -o /tmp/apache-maven.tar.gz https://archive.apache.org/dist/maven/maven-3/3.8.5/binaries/apache-maven-3.8.5-bin.tar.gz \
  && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
  && rm -f /tmp/apache-maven.tar.gz \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn


RUN git clone https://github.com/antlr/antlr4.git \
	&& cd antlr4 \
	&& git checkout 4.9.3 \
 	&& mvn clean --projects tool --also-make \
    && mvn -DskipTests install --projects tool --also-make



RUN cd antlr4 \
	&& mv ./tool/target/antlr4-*-complete.jar /usr/local/lib/ \
	&& cd runtime/Cpp && mkdir build && mkdir run && cd build \
	&& cmake .. -DANTLR_JAR_LOCATION=/usr/local/lib/antlr4-4.9.4-SNAPSHOT-complete.jar \
	&& DESTDIR=../run make install \
	&& cd ../run/usr/local/include \
	&& cp -r antlr4-runtime /usr/local/include \
	&& cd ../lib \
	&& cp -r * /usr/local/lib \
	&& ldconfig

RUN set -eux; \
	apt install -y --no-install-recommends graphviz; \
    pip install boto3; \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"; \
    unzip awscliv2.zip; \
    ./aws/install; \
    aws --profile default configure set aws_access_key_id "$s3_pub_key"; \
    aws --profile default configure set aws_secret_access_key "$s3_prv_key";

RUN set -eux; \
    echo '#!/bin/bash\nCLASSPATH="/usr/local/lib/antlr4-4.9.4-SNAPSHOT-complete.jar:." exec "java" -jar  /usr/local/lib/antlr4-4.9.4-SNAPSHOT-complete.jar "$@"' > /usr/bin/antlr \
    && chmod +x /usr/bin/antlr;

RUN set -eux;  \
    apt install -y --no-install-recommends flex bison \
    && git clone https://github.com/portersrc/spim-keepstats \
    && cd spim-keepstats/spim \
    && make \
    && make install;

ADD source/run_autograder /autograder/run_autograder

# Ensure that scripts are Unix-friendly and executable
RUN chmod +x /autograder/run_autograder; \
     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*