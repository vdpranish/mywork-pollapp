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
                   $('.error-').html(error.message)
               });
               return;
           }
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val()
            if(nonce){
            $.ajax({
                url: '/ajaxaction/',
                type:"POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    action:"payment",
                    nonce:nonce,
                    error:errors
                },
                dataType: "json",
                success: function (data){
                    console.log(data)
//                    if(!data.status){
//                        $('.error-').html(data.message)
//                    }
                }
            });
            }
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


