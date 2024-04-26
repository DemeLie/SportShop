document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');

    searchButton.addEventListener('click', function () {
        if (searchInput.style.display === 'none' || searchInput.style.display === '') {
            searchInput.style.display = 'block';
        } else {
            document.getElementById('searchForm').submit();
        }
    });
});


window.addEventListener("scroll", function () {
    var navbar = document.querySelector(".second-navbar");
    var body = document.querySelector("body");
    if (window.scrollY > 220) {
        navbar.classList.add("fixed-top");
        body.style.paddingTop = navbar.offsetHeight + "px";
    } else {
        navbar.classList.remove("fixed-top");
        body.style.paddingTop = 0;
    }
});
function adjustFooterPosition() {
    var body = document.querySelector("body");
    var footer = document.getElementById("footer");

    var windowHeight = window.innerHeight;
    var bodyHeight = body.offsetHeight;

    if (windowHeight >= bodyHeight + footer.offsetHeight/2) {
        footer.classList.add("fixed-bottom");
        body.style.paddingBottom = footer.offsetHeight + "px";
    } else {
        footer.classList.remove("fixed-bottom");
        body.style.paddingBottom = 0;
    }
}


document.addEventListener("DOMContentLoaded", function() {
    adjustFooterPosition();

    window.addEventListener("scroll", adjustFooterPosition);
});





document.getElementById('load-more-btn').addEventListener('click', function () {
    console.log("Button clicked!");
    var offset = document.querySelectorAll('.items').length;
    fetch(`/load-more-items/?offset=${offset}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);

            var container = document.querySelector('.items-row');
            data.forEach(item => {

                var card = document.createElement('div');
                card.classList.add('col-md-3', 'items');

                var cardLink = document.createElement('a');
                cardLink.classList.add('text-dark', 'text-decoration-none');
                cardLink.href = item.detail_url;


                var cardDiv = document.createElement('div');
                cardDiv.classList.add('card', 'card-add-border');

                var img = document.createElement('img');
                img.classList.add('card-img-top', 'add-border');
                img.id = 'c-img';
                img.src = item.image;
                img.alt = item.name;
                img.style.maxWidth = '350px';
                img.style.height = '300px';


                var cardBody = document.createElement('div');
                cardBody.classList.add('card-body');

                var title = document.createElement('h5');
                title.classList.add('card-title');
                title.textContent = item.name.charAt(0).toUpperCase() + item.name.slice(1);


                var price = document.createElement('p');
                price.classList.add('card-text');
                price.textContent = '$' + item.price;

                var footer = document.createElement('div');
                footer.classList.add('card-footer');
                footer.style.borderRadius = '0 0 20px 20px';

                var small = document.createElement('small');
                small.classList.add('text-muted');
                small.textContent = 'Created ' + item.created_at;

                cardBody.appendChild(title);
                cardBody.appendChild(price);
                footer.appendChild(small);
                cardDiv.appendChild(img);
                cardDiv.appendChild(cardBody);
                cardDiv.appendChild(footer);
                cardLink.appendChild(cardDiv);
                card.appendChild(cardLink);
                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error:', error));
});





