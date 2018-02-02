var blessed = require('blessed')
, screen = blessed.screen();

var sel = new blessed.list({
  top: '0',
  left: '0',
  width: 10,
  height: 'shrink',
  mouse: true,
  keys: true,
  vi: true,
  border: 'line',
  items: ['Item-0','Item-1','Item-2','Item-3','Item-4','Item-5','Item-6'],
  style: {
    fg: 'white',
    bg: 'magenta',
    border: {
      fg: '#f0f0f0'
    },
    hover: {
      bg: 'green'
    }
  }
});
function bilog() {
    var args = Array.prototype.slice.call(arguments);
    require('fs').appendFileSync('/data/github/balance/src/test.log', args.join(',')+'\n');
}
sel.on('select', (a,b,c)=>{
    bilog('select,',a,b,c);
});
sel.on('cancel', (a,b,c)=>{
    bilog('cancel,',a,b,c);
});
sel.on('action', (a,b,c)=>{
    bilog('action,',a,b,c);
});
screen.append(sel);

screen.key(['escape', 'q', 'C-c'], function(ch, key) {
  screen.destroy();
  return process.exit(0);
});
screen.render();

sel.select(4);
screen.render();
