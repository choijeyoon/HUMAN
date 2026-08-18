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

// Issue 001 cover bootstrap. The image payload is stored as verified UTF-8 chunks
// so GitHub Pages never has to serve a repository binary for the hero image.
const issueCover=document.querySelector('.issue-cover-visual');
if(issueCover){
  const media=document.createElement('div');
  media.className='cover-media';
  media.dataset.coverMedia='';
  media.setAttribute('role','img');
  media.setAttribute('aria-label','Editorial composite of a central human portrait, a distant performance crowd and an abstract artificial profile.');
  issueCover.prepend(media);

  const coverStyle=document.createElement('link');
  coverStyle.rel='stylesheet';
  coverStyle.href='assets/cover-v5.css?v=5';
  document.head.appendChild(coverStyle);

  const coverScript=document.createElement('script');
  coverScript.src='assets/cover-loader.js?v=5';
  coverScript.defer=true;
  document.body.appendChild(coverScript);
}
