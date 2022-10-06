This is my solution for a problem posed to job applicants by RGM Advisors, a now defunct trading firm. 
The premise of the problem is to write a code which informs clients——once there are enough orders for a given stock
matching their desired number of shares——how much income, or expense, they would have should they buy, or sell, shares. 
Further, the client needs to be updated continuously as new orders come in regarding their potential income/expense. A
full description of the problem can be found here:

https://web.archive.org/web/20141023152658/http://www.rgmadvisors.com/problems/orderbook/

The file containing the solution code is pricer.py. The test.py file is where I tested out some of my codes
before implementing them in pricer.py. The data used for this problem can be found in pricer.txt.

Lastly, the example given on the website as a comparison test is inconsistent with the data file given to download. 

For example, according to the website's example, the first 20 entries are as follows:

28800538 A b S 44.26 100
28800562 A c B 44.10 100
28800744 R b 100
28800758 A d B 44.18 157
28800773 A e S 44.38 100
28800796 R d 157
28800812 A f B 44.18 157
28800974 A g S 44.27 100
28800975 R e 100
28812071 R f 100
28813129 A h B 43.68 50
28813300 R f 57
28813830 A i S 44.18 100
28814087 A j S 44.18 1000
28814834 R c 100
28814864 A k B 44.09 100
28815774 R k 100
28815804 A l B 44.07 175
28815937 R j 1000
28816245 A m S 44.22 100

However, from the data provided for download, the first 20 entries are as follows:

28800538 A b S 44.26 100
28800562 A c B 44.10 100
28800744 R b 100
28800758 A d B 44.18 157
28800773 A e S 44.38 100
28800796 R d 157
28800812 A f B 44.18 157
28800974 A g S 44.27 100
28800975 R e 100
28812071 R f 157
28813129 A h B 43.68 50
28813830 A i S 44.18 100
28814087 A j S 44.18 1000
28814834 R c 100
28814864 A k B 44.09 100
28815774 R k 100
28815804 A l B 44.07 100
28815937 R j 1000
28816244 R l 100
28816245 A m S 44.22 100

I have modified the data in pricer.txt to be consistent with the example given on the website. 
