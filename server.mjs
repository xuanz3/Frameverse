// Minimal dependency-free local preview server for FRAMEVERSE.
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.PORT || 8000);
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.webp':'image/webp','.svg':'image/svg+xml','.txt':'text/plain; charset=utf-8','.xml':'application/xml; charset=utf-8'};
http.createServer(async (req,res)=>{
  if(req.method!=='GET' && req.method!=='HEAD'){res.writeHead(405).end();return;}
  try{
    const uri=new URL(req.url,'http://localhost');
    const pathname=decodeURIComponent(uri.pathname);
    const pathnameNormalized=pathname==='/'?'/index.html':pathname;
    const file=resolve(root,'.'+pathnameNormalized);
    if(!(file===root||file.startsWith(root+sep))){res.writeHead(403).end();return;}
    const info=await stat(file);
    if(!info.isFile())throw Error('Not a file');
    const data=await readFile(file);
    res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
    res.end(req.method==='HEAD'?undefined:data);
  }catch{res.writeHead(404,{'Content-Type':'text/plain; charset=utf-8'}).end('Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`FRAMEVERSE available at http://localhost:${port}`));
