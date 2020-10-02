// const success = document.querySelector('#sucess')
// const error = document.querySelector('#error')
// error.style.display = "none";
// success.style.display="none";
const paymentForm = new SqPaymentForm({
       //TODO: Replace with your sandbox application ID
       applicationId: "sandbox-sq0idb-5pFqf_ZfCIPuS0DfaUlZkQ",
       inputClass: 'sq-input',
       autoBuild: false,
       inputStyles: [{
           fontSize: '16px',
           lineHeight: '24px',
           padding: '16px',
           placeholderColor: '#a0a0a0',
           backgroundColor: 'transparent',
       }],
       // Initialize the credit card placeholders
       cardNumber: {
           elementId: 'sq-card-number',
           placeholder: 'Card Number'
       },
       cvv: {
           elementId: 'sq-cvv',
           placeholder: 'CVV'
       },
       expirationDate: {
           elementId: 'sq-expiration-date',
           placeholder: 'MM/YY'
       },
       postalCode: {
           elementId: 'sq-postal-code',
           placeholder: 'Postal'
       },
       callbacks: {
           cardNonceResponseReceived: function (errors, nonce, cardData) {
           if (errors) {
               console.error('Encountered errors:');
               errors.forEach(function (error) {
                   console.error('  ' + error.message);
                   document.querySelector('.details-').value = error.message
               });
               // alert('Encountered errors, check browser developer console for more details');
               // success.style.display ="none";
               // setTimeout(function (){error.style.display = "block"},3000)

               return;
           }
              alert(`The generated nonce is:\n${nonce}`);
              document.getElementById('card-nonce').value = nonce;
           // setTimeout( function () {success.style.display ="block"},3000)

               // error.style.display = "none";
           }
       }
     });

 paymentForm.build()

function onGetCardNonce(event) {
       // Don't submit the form until SqPaymentForm returns with a nonce
       event.preventDefault();
       // Request a nonce from the SqPaymentForm object
       paymentForm.requestCardNonce();

     }



let csrftoken = $('input[name=csrfmiddlewaretoken]').val()
 $('#sq-creditcard').click(function (){
     const price = $("#amount").val()
        $.ajax({
            url: '/ajaxaction/',
            type:"POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
                action:"payment",
                nonce:$('#card-nonce').val(),
                price:price,
            },
            dataType: "json",
            success: function (data){
                console.log(data)
                if(!data.status){
                    $('.error-').html(data.message)
                    // $('.details-').html(data.detail)

                }
            }
        });
    }
    )


