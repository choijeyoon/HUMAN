document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());

const paths={
  love:['Attachment','Reward','Prediction'],
  ai:['Cognition','Agency','Consciousness'],
  kpop:['Identity','Attachment','Synchrony'],
  attention:['Reward','Prediction','Effort'],
  society:['Identity','Threat','Status'],
  consciousness:['Awareness','Integration','Prediction']
};

document.querySelectorAll('[data-path]').forEach(el=>{
  const key=el.dataset.path;
  if(paths[key]) el.textContent=paths[key].join(' → ');
});
