

    let mic = document.getElementById('voicebutton');

	let search = document.getElementById('search');
	let product =  document.querySelectorAll('.product');
    let mic_stop = document.querySelector('.stop')


    // check browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;



    if(SpeechRecognition) { // occurs only when browser support for speech recognition
        const recognition = new SpeechRecognition();
        console.log('Your Browser support speech Recognition');
        let micbtn = document.getElementById('voicebutton');
        micbtn.innerHTML = '<i class="bi bi-mic-fill" id="voice-search"></i>'; // add a microphone button only when the browser supports it



        mic.addEventListener('click', micBtnClicked);
        let micIcon = document.getElementById('voice-search')

        function micBtnClicked() {
            if (micIcon.classList.contains('bi-mic-fill')) { // start of speech recognition
                micIcon.classList.remove('bi-mic-fill');
                micIcon.classList.add('bi-mic-mute-fill')
                //Clear all the input in the search box while showing all the products when the user tries to usr voice recognition
                search.value =''
                for(let list_ of product) {
                     list_.style.display = "";
                 }

                recognition.start()

                recognition.onresult = function(e){
                    const m = search.value = e.results[0][0].transcript;
                    showItem(m.toLowerCase());
                    micIcon.classList.remove('bi-mic-mute-fill');
                    micIcon.classList.add('bi-mic-fill')
                    recognition.stop()

                }


            } else {
                micIcon.classList.remove('bi-mic-mute-fill');
                micIcon.classList.add('bi-mic-fill')
                recognition.stop()
            }
        }

    }


    else{
        console.log('Your Browser does not support speech Recognition')
    }


    // would occur even when there is no speech recognition
    //search bar
    // search.onkeyup = ()=> {
    //     const x = search.value.toLowerCase();
    //     showItem(x);
    // }
    search.addEventListener('keyup', ()=>{
        const x = search.value.toLowerCase();
        showItem(x);
    })

    search.addEventListener('search', ()=>{
         for(let list_ of product) {
             list_.style.display = "";
         }


    })


    function showItem(x) {
        for(let list of product) {
            let product = list.children[0].children[1].children[0].innerText;
            let name = product.toLowerCase();
            if (name.search(x) > -1) {
                list.style.display = "";
            }
            else {
                list.style.display = "none";
            }
        }
    }






