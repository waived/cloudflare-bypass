  /////////////////////////////////////////////
 /// CLOUDFLARE CDN/WAF DDOS BYPASS SCRIPT ///
/////////////////////////////////////////////

Overview:
Because of the increased need for security, many modern websites implement some
sort of reverse-proxy technology. At the forefront of this technology, is most
commonly found: CloudFlare. This organization offers many reverse-proxy services
such as Cloudflare's CDN (Content Delivery Network) and WAF (Web Application
Firewall). Instead of a domain pointing to the IP Address of the "origin server"
(the true device an attack is attempting to attack) the domain points to one of
these services.

This means each request sent must be inspected and assuming its not malicious or
malformed in any way, will be passed to the origin server. That request is processed,
sent to the reverse proxy, and the reverse proxy then sends the response back to the
client.

During instances of abuse (DDoS, wordlist attacks, URL tampering, etc) Cloudflare
will begin blocking these requests, either throwing them out altogether or by
enabling rate-limit techniques to buffer an over-influx of traffic. This can
easily defeat basic HTTP-based Denial-of-Service attacks.

This script however aims to bypass Cloudflare services and the many techniques
implemented when trying to mitigate HTTP DDoS attacks. It uses proxification
(via public SOCKS4 proxies), header randomization, and a finite amount of requests
per utilized proxy to forward dynamic and abusive HTTP traffic directly to the
origin server. Because each request is unique (random user-agent, URL refer, etc)
the requests will not be cached and will always take up server-side resources
at the origin.

Note:
This script can also bypass Cloudflare UAM (Under Attack Mode). Although this
script is designed to be used against Cloudflare services, it also works against
services belonging to Akamai, BlazingFast, Amazon CloudFront (part of AWS), etc.

Requirements:
This script requires a few Python libraries to run that may not be installed on
your system. These requirements can be found in the "requirements.txt" file.

They can be installed via: "pip install -r requirements.txt"

Or by manually installing the latest version:
        pip install requests[socks]
        pip install PySocks
