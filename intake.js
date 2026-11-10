'use strict';
(async()=>{
 const host=document.querySelector('#intake');if(!host)return;
 const kind=host.dataset.kind;let invitation=new URLSearchParams(location.hash.slice(1)).get('invite');
 if(invitation)history.replaceState(null,'',location.pathname+location.search);
 let page=0,answers={},enabled=false,demo=false;
 const status=document.querySelector('#intake-status');
 try{
  const r=await fetch(`questionnaires/${kind}.json`);if(!r.ok)throw Error();const schema=await r.json();
  const cfg=await fetch('privacy-config.json').then(r=>r.json());demo=cfg.demo_enabled===true;
  if(cfg.api_enabled&&cfg.approved&&invitation){const r=await fetch('/api/intake-status',{credentials:'same-origin'});if(r.ok){const result=await r.json();enabled=result.enabled&&result.version===schema.version}}
  status.textContent=enabled?'Заполняйте анкету только за себя. Данные не сохраняются в браузере.':demo?'Демо для знакомства с анкетой. Используйте тестовые данные: ответы остаются только в памяти этой вкладки и никуда не отправляются.':'Пока доступен только просмотр вопросов.';
  function save(){for(const q of schema.pages[page].items){if(q.type==='comment')continue;const nodes=[...host.querySelectorAll(`[name="${q.id}"]`)];if(q.type==='enum')answers[q.id]=nodes.filter(n=>n.checked).map(n=>n.value);else if(q.type==='boolean'){const selected=nodes.find(n=>n.checked);answers[q.id]=selected?selected.value==='yes':null;}else {const value=nodes[0]?.value||'';answers[q.id]=q.type==='integer'&&value!==''?Number(value):value}}}
  function render(){
   host.replaceChildren();const progress=document.createElement('p');progress.className='intake-progress';progress.textContent=`Раздел ${page+1} из ${schema.pages.length}`;host.append(progress);
   const form=document.createElement('form');form.autocomplete='off';
   const fields=document.createElement('fieldset');fields.className='intake-fieldset';fields.disabled=!(enabled||demo);
   for(const q of schema.pages[page].items){
    if(q.type==='comment'){const el=document.createElement(q.header?'h2':'p');el.textContent=q.label;fields.append(el);if(q.comment){const p=document.createElement('p');p.textContent=q.comment;fields.append(p)}continue}
    const box=document.createElement('div');box.className='intake-field';const required=q.validations?.some(v=>v.type==='required');
    const label=document.createElement('label');label.htmlFor=q.id;label.textContent=q.label+(required?' *':'');box.append(label);
    if(q.type==='enum'||q.type==='boolean'){
     label.removeAttribute('for');box.setAttribute('role','group');box.setAttribute('aria-label',q.label);
     const choices=q.type==='boolean'?[{id:'yes',label:'Да'},{id:'no',label:'Нет'}]:q.items;
     for(const option of choices){const wrapper=document.createElement('label');wrapper.className='choice';const input=document.createElement('input');input.name=q.id;input.type=q.type==='enum'&&q.widget==='checkbox'?'checkbox':'radio';input.value=option.id;
      input.checked=q.type==='boolean'?(answers[q.id]===true&&option.id==='yes')||(answers[q.id]===false&&option.id==='no'):(answers[q.id]||[]).includes(option.id);wrapper.append(input,document.createTextNode(option.label.trim()));box.append(wrapper)}
    }else{const input=document.createElement(q.multiline?'textarea':'input');input.name=q.id;input.id=q.id;input.required=required&&enabled;input.maxLength=5000;if(q.type==='integer'){input.type='number';input.step='1';for(const v of q.validations||[]){if(v.type==='min')input.min=v.value;if(v.type==='max')input.max=v.value}}input.value=answers[q.id]??'';box.append(input)}
    fields.append(box);
   }
   form.append(fields);
   if(page===schema.pages.length-1&&enabled){const label=document.createElement('label');label.className='choice';const checkbox=document.createElement('input');checkbox.type='checkbox';checkbox.required=true;checkbox.disabled=!enabled;const span=document.createElement('span');span.innerHTML='Даю <a href="consent.html" target="_blank" rel="noopener">отдельное согласие на обработку данных этой анкеты</a>. Специальное письменное согласие оформлено отдельно до получения приглашения.';label.append(checkbox,span);form.append(label)}
   const navigation=document.createElement('div');navigation.className='intake-navigation';
   if(page){const back=document.createElement('button');back.type='button';back.className='intake-button';back.textContent='Назад';back.onclick=()=>{if(enabled||demo)save();page--;render()};navigation.append(back)}
   const next=document.createElement('button');next.className='intake-button';next.type='submit';next.textContent=page<schema.pages.length-1?'Далее':enabled?'Отправить анкету':demo?'Посмотреть заполненную анкету':'Приём пока не открыт';next.disabled=page===schema.pages.length-1&&!(enabled||demo);navigation.append(next);form.append(navigation);
   const error=document.createElement('p');error.className='intake-error';error.setAttribute('role','status');form.append(error);host.append(form);
   form.onsubmit=async event=>{
    event.preventDefault();if(enabled){
     for(const q of schema.pages[page].items){if((q.type==='enum'||q.type==='boolean')&&q.validations?.some(v=>v.type==='required')&&!form.querySelector(`[name="${q.id}"]:checked`)){error.textContent='Ответьте на обязательные вопросы.';return}}
     save();
    }
    if(demo&&!enabled)save();
    if(page<schema.pages.length-1){page++;render();host.scrollIntoView({behavior:'instant'});return}
    if(!enabled&&demo){
     host.replaceChildren();const heading=document.createElement('h2');heading.textContent='Предпросмотр вашей анкеты';host.append(heading);
     const note=document.createElement('p');note.textContent='Демонстрация завершена. Ответы не отправлены и не сохранены на сервере.';host.append(note);
     for(const section of schema.pages)for(const q of section.items){if(q.type==='comment')continue;let value=answers[q.id];if(value===undefined||value===null||value===''||Array.isArray(value)&&!value.length)continue;
      if(q.type==='enum'){const names=Object.fromEntries(q.items.map(i=>[i.id,i.label]));value=value.map(v=>names[v]).join(', ')}else if(q.type==='boolean')value=value?'Да':'Нет';
      const title=document.createElement('h3');title.textContent=q.label;const p=document.createElement('p');p.textContent=String(value);host.append(title,p);
     }
     const reset=document.createElement('button');reset.className='intake-button';reset.textContent='Очистить и начать заново';reset.onclick=()=>{answers={};page=0;render()};host.append(reset);host.scrollIntoView({behavior:'instant'});return;
    }
    if(!enabled)return;next.disabled=true;
    try{const r=await fetch(`/api/questionnaires/${kind}`,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+invitation},body:JSON.stringify({version:schema.version,answers,privacy_consent:true}),credentials:'same-origin'});if(!r.ok)throw Error();const result=await r.json();answers={};invitation=null;host.replaceChildren();const p=document.createElement('p');p.textContent='Анкета принята. Номер: '+result.id;host.append(p)}catch{error.textContent='Анкета не отправлена. Проверьте связь или срок приглашения и повторите попытку.';next.disabled=false}
   };
  }
  addEventListener('pagehide',()=>{answers={};host.replaceChildren()});
  render();
 }catch{status.textContent='Не удалось загрузить вопросы. Обновите страницу позже.'}
})();
