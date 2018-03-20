---
layout: post
date: 2017-08-29 08:14:51.556228
title: Como hacer un Proxy de Tor con un Raspberry Pi
author: oschvr
mail: os@oschvr.com
excerpt: Un tutorial sobre como hacer un proxy de Tor con un Raspberry Pi 2 y Raspbian Jessie, para navegar anon.
tags: tor, raspberry, proxy, raspberry pi, pi, tor pi, raspian
lang: es_MX
image: https://s3-us-west-2.amazonaws.com/oscarchavez/posts/como-hacer-un-proxy-de-tor-con-un-raspberry-pi/images/large/tor-network-.jpg
---

![cover](https://oschvr.com/static/oscarchavez/img/torproxy/cover.png)

> Por [@oschvr](https://twitter.com/oschvr)

---

## [Descarga el PDF](https://oschvr.com/static/oscarchavez/img/torproxy/torproxy.pdf)
{: style="text-align: center;"}

---

### Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/Rl4kKxOOsgU?rel=0" frameborder="0" allowfullscreen></iframe>

![rpi](https://oschvr.com/static/oscarchavez/img/torproxy/rpi.jpg)
{: style="max-width: 55%;"}

### Requisitos

- Raspberry Pi (2 o 3)
- ISO de Raspbian Jessie (Debian) [Descargar](https://www.raspberrypi.org/downloads/raspbian/)
- Tarjeta SD > 8Gb (SDCard)
- Tarjeta Inalámbrica (Wifi Dongle)
- Conexión a Router por Ethernet
- Periféricos (Teclado, Mouse, Monitor, Cable HDMI)

## Iniciando

1. Flashear el ISO de Raspbian a la SDCard. Yo usé [ApplePi Baker](http://macappstore.org/applepi-baker/). Aquí hay un [excelente tutorial](https://computers.tutsplus.com/articles/how-to-flash-an-sd-card-for-raspberry-pi--mac-53600)
2. Conectar todos los periféricos (mouse, teclado, monitor) y el micro Usb
para encender el Raspberry
3. Abrir una terminal y escribir `sudo raspi-config`
4. Ir a `'Interfacing Options' > 'SSH'` y habilitar el server de SSH y salir.
5. Escribir `ifconfig` y copiar la dirección IP que está a un lado de `inet` en la parte de `eth0`

![ssh](https://oschvr.com/static/oscarchavez/img/torproxy/ssh.png)

## Tutorial

Primero que nada, establecemos la conexión a nuestro RaspberryPi por medio de *SSH*

Abrimos nuestra terminal y tecleamos:

```
ssh pi@<dirección IP que conseguimos en el paso anterior>
```

en mi caso es:

```
ssh pi@192.168.100.5
```


Y escribimos la contraseña, que por default es `raspberry`.

Actualizamos los paquetes

```
sudo apt-get update
```

#### HOSTAPD y ISC-DHCP-SERVER

Instalamos hostapd y isc-dhcp-server

```
sudo apt-get install hostapd isc-dhcp-server
```

Instalamos iptables-persistent

```
sudo apt-get install iptables-persistent
sudo nano /etc/dhcp/dhcpd.conf
```

Encontrar las lineas que dicen

```
option domain-name "example.org";
option domain-name-servers ns1.example.org, ns2.example.org;
```

Comentarlas (ponerles un # al principio)

```
 # option domain-name "example.org";
 # option domain-name-servers ns1.example.org, ns2.example.org;
```

Encontrar las lineas que dicen

```
 # If this DHCP server is the official DHCP server for the local
 # network, the authoritative directive should be uncommented.
 #  authoritative;
```

Y quitar el #

```
 # If this DHCP server is the official DHCP server for the local
 # network, the authoritative directive should be uncommented. 
  authoritative;
```

Baja, agrega lo siguiente y guarda:

```
subnet 192.168.42.0 netmask 255.255.255.0 {
  range 192.168.42.10 192.168.42.50;
  option broadcast-address 192.168.42.255;
  option routers 192.168.42.1;
  default-lease-time 600;
  max-lease-time 7200;
  option domain-name "local";
  option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

```
sudo nano /etc/default/isc-dhcp-server
```

Baja a INTERFACES="" y actualiza a INTERFACES="wlan0"

```
sudo ifdown wlan0
sudo nano /etc/network/interfaces
```

Cambia manual por dhcp en iface eth0

Quita cualquier configuracion de wlan0, agrega lo siguiente y guarda:

```
auto lo

iface lo inet loopback 
iface eth0 inet dhcp

allow-hotplug wlan0

iface wlan0 inet static
 address 192.168.42.1
 netmask 255.255.255.0

 #iface wlan0 inet manual
 #wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
 #iface default inet dhcp
```

Asignale la ip estatica a wlan0

```
sudo ifconfig wlan0 192.168.42.1
sudo nano /etc/hostapd/hostapd.conf
```

Copia y pega la siguiente configuración de hostapd, recuerda cambiar el `ssid` y el `wpa_passphrase`.

```
interface=wlan0
 #driver=rtl871xdrv
ssid=TORNet
country_code=US
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=Raspberry
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
wpa_group_rekey=86400
ieee80211n=1
wme_enabled=1
```

```
sudo nano /etc/default/hostapd
```

Encuentra #DAEMON_CONF="" para que diga DAEMON_CONF="/etc/hostapd/hostapd.conf"

```
sudo nano /etc/init.d/hostapd
```

Vuelve a hacer lo mismo en, DAEMON_CONF="" para que diga DAEMON_CONF="/etc/hostapd/hostapd.conf"

```
sudo nano /etc/sysctl.conf
```

Descomenta la linea: `net.ipv4.ip_forward=1`

Cambia las tablas de IP a lo siguiente:

```
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables/rules.v4"
```

Levantamos para probar nuestro punto de acceso:

```
sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf
```

Deberíamos ver nuestro ssid en la lista de redes.

```
sudo mv /usr/share/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service ~/
```

Reiniciamos hostapd e isc-dhcp-server y con [update-rc.d](https://www.debuntu.org/how-to-managing-services-with-update-rc-d/) para iniciarlos al reiniciar el raspberry

```
sudo reboot
sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf
sudo service hostapd start
sudo service isc-dhcp-server start
sudo update-rc.d hostapd enable
sudo update-rc.d isc-dhcp-server enable
```

Revisamos si ambos estan arriba.

```
sudo service isc-dhcp-server status
sudo service hostapd status
```

![services](https://oschvr.com/static/oscarchavez/img/torproxy/services.png)

#### TOR

```
sudo apt-get update
sudo apt-get install tor
sudo nano /etc/tor/torrc
```

e inserta lo siguiente en alguna parte de arriba del archivo:

```
Log notice file /var/log/tor/notices.log
VirtualAddrNetwork 10.192.0.0/10
AutomapHostsSuffixes .onion,.exit
AutomapHostsOnResolve 1
TransPort 9040
TransListenAddress 192.168.42.1
DNSPort 53
DNSListenAddress 192.168.42.1
```
Cambia las tablas de IP para rutear hacia el puerto 9040 de TOR.

```
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 22 -j REDIRECT --to-ports 22
sudo iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j REDIRECT --to-ports 53
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --syn -j REDIRECT --to-ports 9040
sudo iptables -t nat -L
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

Reconfiguramos iptables-persistent para usar las reglas actuales

```
sudo dpkg-reconfigure iptables-persistent
```

Creamos los logs de tor y les cambiamos el *owner* y el *mode* 

```
sudo touch /var/log/tor/notices.log
sudo chown debian-tor /var/log/tor/notices.log
sudo chmod 644 /var/log/tor/notices.log
ls -l /var/log/tor
```

Iniciamos el servicio de tor y lo hacemos automático al inico del RPi.

```
sudo service tor start
sudo service tor status
sudo update-rc.d tor enable
```

#### Prueba

![ssid](https://oschvr.com/static/oscarchavez/img/torproxy/ssid.png)

Nos conectamos a la red desde otra computadora o teléfono para probar, y visitamos [https://check.torproject.org/](https://check.torproject.org/) para comprobar conexión a internet y que en efecto nuestro tráfico esta siendo routeado por Tor.

--

[¿Qué es y cómo usar Tor?](https://www.youtube.com/watch?v=wlP1JrfvUo0&t=45s)


![hexagons](https://oschvr.com/static/oscarchavez/img/torproxy/hexagons.png)