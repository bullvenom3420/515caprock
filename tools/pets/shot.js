const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch();
for (const [n,w,h] of [['dog',600,792],['cat',560,736]]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 await p.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync(n+'.svg','utf8')+'</body></html>');
 await p.screenshot({path:n+'.png',omitBackground:true,clip:{x:0,y:0,width:w,height:h}}); await p.close();}
await b.close();})();
