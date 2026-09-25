/* Presentation vocabulary v1. Raw files and trained model artifacts stay unchanged. */
(()=>{const key=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().replace(/\s+/g,' ').toUpperCase();
const rules={'OURO':'Ouro','MINERIO DE OURO':'Ouro','FERRO':'Minério de ferro','MINERIO DE FERRO':'Minério de ferro'};
function names(v){if(typeof v!=='string')return v;const seen=new Set();return v.split(/\s*;\s*|\s+\/\s+/).map(t=>rules[key(t)]||t.trim()).filter(t=>{const k=key(t);if(!t||seen.has(k))return false;seen.add(k);return true}).join('; ')}
window.mineralNames=names;
window.normalizeMinerals=function(data,url=''){
 const path=new URL(url||location.href,location.href).pathname;
 if(/\/stock\/\d+\.json$/.test(path)){for(const row of data){row[13]=row[4];row[4]=names(row[4])}return data}
 if(path.endsWith('/characteristics.json')){for(const row of Object.values(data)){row[13]=row[4];row[4]=names(row[4])}return data}
 function walk(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)){o.forEach(walk);return}for(const k of Object.keys(o)){if(['sub','substancias','substancias_cadastradas','Substancia'].includes(k)&&typeof o[k]==='string'){o[k+'_original']=o[k];o[k]=names(o[k])}else if(!k.endsWith('_original'))walk(o[k])}}
 walk(data);return data;
};
const nativeFetch=window.fetch;window.fetch=async function(input,options){const response=await nativeFetch(input,options);const u=new URL(typeof input==='string'?input:input.url,location.href);if(u.origin===location.origin&&u.pathname.endsWith('.json')){const parse=response.json.bind(response);response.json=async()=>normalizeMinerals(await parse(),u.href)}return response};
})();
