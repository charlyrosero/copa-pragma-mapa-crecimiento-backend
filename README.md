ec2-18-212-205-152.compute-1.amazonaws.com

ssh -i "/Users/charly.rosero/Apps/copa-pragma/tunnel-ssh.pem" ec2-user@ec2-18-212-205-152.compute-1.amazonaws.com

ssh -i "tunnel-ssh.pem" 


ssh -i "/Users/charly.rosero/Apps/copa-pragma/tunnel-ssh.pem" -L 27017:mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017 ec2-user@ec2-3-93-168-214.compute-1.amazonaws.com -N 

ssh -i "/Users/charly.rosero/Apps/copa-pragma/tunnel-ssh.pem" -L 27017:mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017 ec2-user@3.93.168.214 -N 




mongodb://pragma:<insertYourPassword>@mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017/?retryWrites=false


ssh -i "/Users/charly.rosero/Apps/copa-pragma/admonhost_mc.pem" -L 27017:mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017 ec2-user@3.87.236.148 -N

ssh -i "admonhost_mc.pem" -L 27017:copapragmadb.cluster-cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017 ec2-user@3.87.236.148 -N