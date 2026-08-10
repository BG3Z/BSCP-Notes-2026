
1. Change Host Header to your exploit server to exfiltrate password reset token

2. Bypass authorization by setting Host: localhost

3. Add a Second 'Host' Header reflected in response -> Cache Poisoning
![[Pasted image 20260731165731.png]]

4. SSRF to access admin panel somewhere in 192.168.1.0/24:
	* Uncheck 'Update Host Header to match target' on Intruder:
	* Host: 192.168.0.§1§
	* Bruteforce 1 to 255 and access admin panel

5. You can add full URL as GET https://lab/ and then set arbitrary 'Host' header:
![[Pasted image 20260731171654.png]]

6. Duplicate request with GET /admin and Host 192.168.0.1 and send in **SEQUENCE** (in the exam it would be probably localhost:6566):
![[Pasted image 20260731172533.png|299]]
* First Request:
![[Pasted image 20260731172548.png]]
* Second Request:
![[Pasted image 20260731172716.png]]

