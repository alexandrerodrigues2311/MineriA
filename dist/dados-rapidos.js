/* Lossless transport; original JSON remains the compatibility fallback. */
window.fastJSON=async function(url){
 const supported=new Set(['areas.json','characteristics.json','pesquisa/estoque_apto.json','pesquisa/predicoes_v5.json','pesquisa/trajetorias_v5.json','pesquisa/cubo_gestao.json']);
 const [path,query]=url.split('?');
 if(supported.has(path)&&typeof DecompressionStream!=='undefined'){
  try{const r=await fetch(path+'.gz'+(query?'?'+query:''));if(!r.ok)throw Error();const bytes=new Uint8Array(await r.arrayBuffer());const stream=new Blob([bytes]).stream();return JSON.parse(await new Response(bytes[0]===31&&bytes[1]===139?stream.pipeThrough(new DecompressionStream('gzip')):stream).text())}catch(e){/* Retry the same snapshot without compression. */}
 }
 const r=await fetch(url);if(!r.ok)throw Error('Não foi possível carregar os dados. Tente novamente.');return r.json();
};
