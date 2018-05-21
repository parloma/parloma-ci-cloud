FROM arm32v7/ros:kinetic-ros-base

RUN apt-get update && apt-get install ros-kinetic-rosbridge-suite ros-kinetic-rosserial net-tools python3-pip supervisor -y

RUN apt-get update && \
 apt-get install build-essential checkinstall -y &&\
 apt-get install libssl-dev liblzo2-dev libpam0g-dev wget net-tools -y 
 
RUN wget https://swupdate.openvpn.org/community/releases/openvpn-2.4.4.tar.gz && tar zxvf openvpn-2.4.4.tar.gz
RUN cd openvpn-2.4.4 && ./configure && make && checkinstall -y

COPY ./entrypoint.sh /entrypoint.sh
COPY ./parloma.launch /parloma.launch

RUN pip3 install requests ifcfg 

COPY ./server/requirements.txt /server/requirements.txt
RUN cd /server && pip3 install -r requirements.txt

COPY ./server /server
COPY ./conf/conf.d /etc/supervisor/conf.d
COPY ./conf/rosbridge_init.sh /rosbridge_init.sh
COPY ./develop /develop
COPY ./server/blink.sh /blink.sh

COPY ./entrypoint.sh /
COPY ./parloma.launch /

RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]