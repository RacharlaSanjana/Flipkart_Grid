async function getSimilarUserRecommendations() {
    const userId = document.getElementById('user-id').value;
    fetch('/api/similar_user/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "user_id": userId })
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendation(data.recommendations);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayRecommendation(recommendations) {
    var recommendationsList = document.getElementById("similar-users-recommendations-list");
    console.log(recommendations);
    recommendationsList.innerHTML =``;
    console.log(recommendationsList)
    for (var i = 0; i < recommendations.length; i++) {
        var listItem = document.createElement("li");
        listItem.innerHTML = `
            <img src="${recommendations[i].image_url}" alt="${recommendations[i].product_name}">
            <p>${recommendations[i].product_name}</p>
            <p>Price: ${recommendations[i].price}</p>`;
        recommendationsList.appendChild(listItem);
    }
 }

// Function to fetch similar user recommendations
        // async function getSimilarUserRecommendations() {
        //     const userId = document.getElementById('user-id').value;
        //     fetch('/api/similar_user/recommendations', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //         },
        //         body: JSON.stringify({ "user_id": userId })
        //     })
        //     .then(response => response.json())
        //     .then(data => {
        //         displayRecommendations(data.recommendations);
        //     })
        //     .catch(error => {
        //         console.error('Error:', error);
        //     });
        // }

        // function displayRecommendations(recommendations) {
        //     var recommendationsList = document.getElementById("similar-users-recommendations-list");
        //     console.log(recommendations);
        //     recommendationsList.innerHTML =``;
        //     console.log(recommendationsList)
        //     for (var i = 0; i < recommendations.length; i++) {
        //         var listItem = document.createElement("li");
        //         listItem.innerHTML = `
        //             <img src="${recommendations[i].image_url}" alt="${recommendations[i].product_name}">
        //             <p>${recommendations[i].product_name}</p>
        //             <p>Price: ${recommendations[i].price}</p>`;
        //         recommendationsList.appendChild(listItem);
        //     }
        //  }

        // Function to fetch rank-based recommendations
//         async function getRankBasedRecommendations() {
//             const subCategory = document.getElementById('sub-category').value;

//             try {
//                 const response = await fetch('/api/rank_based/recommendations', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                     body: JSON.stringify({ "sub_category": subCategory })
//                 });
//                 if (response.ok) {
//                     const data = await response.json();
//                     console.log(data);
//                     displayRecommendations('rank-based-recommendations-list', data.recommendations);
//                 } else {
//                     console.error('Error:', response.status, response.statusText);
//                 }
//             } catch (error) {
//                 console.error('Error:', error);
//             }
//         }

//         // // Function to fetch model-based recommendations
//         // async function getModelBasedRecommendations() {
//         //     const userIdModel = document.getElementById('user-id-model').value;

//         //     try {
//         //         const response = await fetch('/api/model_based/recommendations', {
//         //             method: 'POST',
//         //             headers: {
//         //                 'Content-Type': 'application/json'
//         //             },
//         //             body: JSON.stringify({ "user_id": userIdModel })
//         //         });

//         //         if (response.ok) {
//         //             const data = await response.json();
//         //             displayRecommendations('model-based-recommendations-list', data.recommendations);
//         //         } else {
//         //             console.error('Error:', response.status, response.statusText);
//         //         }
//         //     } catch (error) {
//         //         console.error('Error:', error);
//         //     }
//         // }

//         // Function to display recommendations in a list
//         function displayRecommendations(listId, recommendations) {
//             const recommendationsList = document.getElementById(listId);
//             recommendationsList.innerHTML = "";

//             for (const product of recommendations) {
//                 const listItem = document.createElement("li");
//                 listItem.innerHTML = `
//                     <img src="${product.image_url}" alt="${product.product_name}" width="200" height="300">
//                     <p>${product.product_name}</p>
//                     <p>Price: ${product.price}</p>`;
//                 recommendationsList.appendChild(listItem);
//             }
//         }