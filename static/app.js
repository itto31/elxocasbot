var tts = window.speechSynthesis;
var synth = window.speechSynthesis;
var voices = synth.getVoices();

class Chatbox{
    
    constructor(){
        
        this.args = {
            chatbox: document.querySelector('.chatbox'),
           sendButton: document.querySelector('.send__button')
        }
        this.state = false;
        this.message = [];
    }

    display(){
        const{sendButton,chatbox} = this.args;
        sendButton.addEventListener('click',()=>this.onSendButton(chatbox))

        const node = chatbox.querySelector('input');
        node.addEventListener('keyup',({key})=>{
            if(key === 'Enter'){
                this.onSendButton(chatbox);
            }
        })
    }
       
        
    onSendButton(chatbox){
        
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 ===""){
            return;
        }
        let msg1 ={name:"Usuario",message:text1};
        this.message.push(msg1);

        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r =>{
            let msg2 = {name:"Paco", message:r.answer};
            this.voice(r.answer);
            this.message.push(msg2);
            this.updateChatText(chatbox);
            textField.value = "";
        }).catch((error)=>{
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = "";
        });
    }


    voice(message){

        var utterThis = new SpeechSynthesisUtterance(message);
        utterThis.voice = voices["Microsoft Helena - Spanish(Spain)"];
        synth.speak(utterThis);
    }

    updateChatText(chatbox){
        
        var html = "";
        
        this.message.slice().reverse().forEach(function(item,index){
            if(item.name === "Paco"){
                html += `
                <div class="display">
                <div class="chatbox__message chatbox__message__right">
                    <img src="../static/fondo/3.png" alt="Paco" class="chatbox__avatar">
                    <div class="flr">
                    <p class="msg">Elxocas: ${item.message}</p>
                    </div>
                </div>
                </div>
                `                
            }
            else{
                html += `
                <div class='chatbox__message chatbox__message__left'>
                    <img src="../static/fondo/2.png" alt="Usuario" class="chatbox__avatar">
                    <div class="flr">
                    <p class="msg">${item.message}</p>
                    </div>
                </div>`
            }
        })
       
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();