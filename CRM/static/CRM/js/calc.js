$(document).ready(function() {

  var currentNum = '';
  var total = 0;
  var operation = '';
  console.log(typeof(total));

  function updateDisplay(disp) {
    console.log('Display updating: '+disp);
    $('p').text(disp);
  }

  function opPush(op) {
    console.log('Operand pushed');
    if (op === 'percent') {
      var currentNumInt = Number(currentNum);
      currentNumInt= currentNumInt / 100;
      currentNum = currentNumInt;
      updateDisplay(currentNumInt);
    } else {
      console.log('else run');
      if (op !== 'ce') {
        var currentNumInt = Number(currentNum);
        if (currentNumInt) {
          switch (operation) {
            case '':
              total = currentNumInt;
              break;
            case 'divide':
              total = total / currentNumInt;
              break;
            case 'times':
              total = total * currentNumInt;
              break;
            case 'minus':
              total = total - currentNumInt;
              break;
            case 'plus':
              total = total + currentNumInt;
              break;
            case 'equals':
              break;
          }
        }
        if (op === 'ca') {
          console.log('CA');
          total = 0;
          op = '';
        }
        console.log('Total = '+total);
        operation = op;
      }
      updateDisplay(total);
      currentNum = '';
    }
  }

  function numPush(num) {
    console.log('Number pushed: '+num);
    currentNum += num;
    if (currentNum === '.') {
      currentNum = '0.';
    }
    updateDisplay(currentNum);
  }

  function buttonPush(btn) {
    console.log('btn = '+btn);
    if (btn === 'decimal') {
      numPush('.');
    } else if (isNaN(btn)) {
      opPush(btn);
    } else {
      numPush(btn);
    }
  }

  // superfluous?
  function updateTotal(op,num) {
  }


  $('button').click(function() {
    var btn = $(this).attr("id");
    console.log('Button pushed: '+btn);
    buttonPush(btn);
  });

  // SHIFT DOESNT CHANGE CHARACTER CODES ??? //
  /*document.addEventListener('keydown', function(event) {
    var keyPress = event.keyCode;
    console.log('Key pressed: '+keyPress);
    var keyChar = String.fromCharCode(keyPress);
    console.log('Key Char: '+keyChar);
    buttonPush(keyChar);
  });*/
})
