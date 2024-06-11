
        // Function to fetch model-based recommendations
        async function getModelBasedRecommendations() {
            const userIdModel = document.getElementById('user-id-model').value;
            const num_recommendations = 10;
        
            const response = await fetch('/api/model_based/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userIdModel,
                    num_recommendations: num_recommendations
                })
            });

            if (response.ok) {
            // console.log(response);
            const data = await response.json();
            // console.log(data.recommended_products);
            const recommendedProducts = data.recommended_products;
            console.log(recommendedProducts);
            const productsList = document.getElementById('model-based-recommendations-list');
            productsList.innerHTML = '';

            for (var i = 0; i < recommendedProducts.length; i++) {
                const listItem = document.createElement('li');
                listItem.innerHTML =`<img src= "${recommendedProducts[i].image}" alt="${recommendedProducts[i].product_name}">
                <p>${recommendedProducts[i].product_name}</p>
                <p>Price: ${recommendedProducts[i].price}</p>`;
                productsList.appendChild(listItem);
            };
        } else {
            console.error('Error:', response.status, response.statusText);
        }
    }


