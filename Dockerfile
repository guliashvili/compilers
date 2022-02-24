FROM gradescope/auto-builds:ubuntu-20.04

RUN set -eux; \
	apt update; \
	apt install -y --no-install-recommends software-properties-common; \
	apt update; \
	add-apt-repository -y ppa:ubuntu-toolchain-r/test; \
	add-apt-repository ppa:linuxuprising/java -y; \
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
		make;
	# update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110 --slave /usr/bin/g++ g++ /usr/bin/g++-11 --slave /usr/bin/gcov gcov /usr/bin/gcov-11 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-11 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-11  --slave /usr/bin/cpp cpp /usr/bin/cpp-11

RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
  && curl -fsSL -o /tmp/apache-maven.tar.gz https://dlcdn.apache.org/maven/maven-3/3.8.4/binaries/apache-maven-3.8.4-bin.tar.gz \
  && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
  && rm -f /tmp/apache-maven.tar.gz \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn


RUN set -eux; \
	git clone https://github.com/antlr/antlr4.git \
	&& cd antlr4 \
	&& git checkout 4.9.3 \ 
 	&& mvn clean --projects tool --also-make \
    	&& mvn -DskipTests install --projects tool --also-make \
    	&& mv ./tool/target/antlr4-*-complete.jar /usr/local/lib/ \
	&& cd runtime/Cpp && mkdir build && mkdir run && cd build \
	&& cmake .. -DANTLR_JAR_LOCATION=/usr/local/lib/antlr4-4.9.3-complete.jar \
	&& DESTDIR=../run make install \
	&& cd ../run/usr/local/include \
	&& cp -r antlr4-runtime /usr/local/include \
	&& cd ../lib \
	&& cp * /usr/local/lib \
	&& ldconfig 
		

ADD source /autograder/source

RUN cp /autograder/source/run_autograder /autograder/run_autograder

# Ensure that scripts are Unix-friendly and executable
RUN chmod +x /autograder/run_autograder