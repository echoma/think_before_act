var blessed = require('blessed')
, screen = blessed.screen();

var box = new blessed.box({
  top: '0',
  left: '0',
  width: '100%',
  tags: true,
  border: {
    type: 'line'
  },
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
screen.append(box);

var top = new blessed.box({
  top: 0,
  left: 0,
  width: `100%-2`,
  shrink: true,
  style: {
    fg: 'white',
    bg: 'blue'
  }
});
box.append(top);

var btn_com = new blessed.button({
  parent: top,
  shrink:true,
  mouse: true,
  border: 'line',
  content: "Component",
  style: {
    fg: 'white',
    bg: 'green',
    border: {
      fg: 'red',
      bg: 'green'
    },
    hover: {
      bg: 'white'
    }
  }
});
//top.append(btn_com);

var btn_set = new blessed.button({
  right: 0,
  shrink:true,
  mouse: true,
  border: 'line',
  content: "Settings",
  style: {
    fg: 'white',
    bg: 'green',
    border: {
      fg: 'red',
      bg: 'green'
    },
    hover: {
      bg: 'white'
    }
  }
});
top.append(btn_set);

screen.key(['escape', 'q', 'C-c'], function(ch, key) {
  screen.destroy();
  return process.exit(0);
});
screen.render();
