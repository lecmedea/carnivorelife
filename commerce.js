'use strict';
(async()=>{
 const status=document.querySelector('#checkout-status');
 try{
  const response=await fetch('site-config.json');
  if(!response.ok)throw Error('catalog');
  const config=await response.json();
  const choice=document.querySelector('#service-choice');
  const requested=new URLSearchParams(location.search).get('service');
  if(config.services.some(s=>s.id===requested))choice.value=requested;
  function render(){
   const service=config.services.find(s=>s.id===choice.value);
   document.querySelector('#checkout-title').textContent=service.title;
   document.querySelector('#checkout-description').textContent=service.intro;
   document.querySelector('#checkout-price').textContent=service.price?`${service.price.toLocaleString('ru-RU')} ₽`:service.price_range||'Стоимость и длительность уточняются до покупки';
   const action=document.querySelector('#checkout-action');
   const documents=document.querySelector('#checkout-documents');
   documents.replaceChildren();
   const payment=service.payment_url?new URL(service.payment_url):null;
   const ready=payment?.protocol==='https:'&&service.price>0&&config.documents.length>0;
   action.classList.remove('is-disabled');action.removeAttribute('aria-disabled');
   if(ready){
    const label=document.createElement('label');label.className='checkout-consent';
    const checkbox=document.createElement('input');checkbox.type='checkbox';
    const text=document.createElement('span');text.textContent='Я ознакомилась с условиями выбранной услуги и документами: ';
    config.documents.forEach(doc=>{const a=document.createElement('a');a.href=doc.url;a.textContent=doc.title+'; ';text.append(a)});
    label.append(checkbox,text);documents.append(label);
    action.href=payment.href;action.textContent='Перейти к оплате ↗';
    function sync(){action.classList.toggle('is-disabled',!checkbox.checked);action.setAttribute('aria-disabled',String(!checkbox.checked))}
    checkbox.addEventListener('change',sync);sync();
    status.textContent='Оплата откроется на защищённой странице платёжного сервиса.';
   }else{
    action.href=config.max_url;action.textContent='Уточнить условия в MAX ↗';
    status.textContent='Онлайн-оплата этой услуги пока не открыта. Алёна уточнит стоимость, условия и дальнейшие шаги лично.';
   }
  }
  choice.addEventListener('change',render);render();
  document.querySelector('#checkout-action').addEventListener('click',e=>{if(e.currentTarget.getAttribute('aria-disabled')==='true')e.preventDefault()});
 }catch{status.textContent='Не удалось загрузить условия. Напишите Алёне в MAX по кнопке выше.'}
})();
