var topButton = document.getElementById("back2top");

window.onscroll = function() {scrollFunction()};
		
function scrollFunction() {
	if(document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
		topButton.style.opacity = 1;
	} else {
		topButton.style.opacity = 0;
	}
}

function smoothScrollToTop() {
	window.scrollTo({top: 0, behavior: "smooth"});
};

$(document).ready(function() {
	
	$('.toCart').click(function() {
		let foodname = $(this).data('name');
		let foodprice = $(this).data('price');

		let html = '<div class="ordered"><div class="remove" title="remove this">X</div>' + foodname +'&emsp; &#8594; &emsp;' + foodprice + '</div>';
		
		$('#cart').children().first().after(html);
		
	})
	
	$('#cart').on('click','.remove',function() {
		$(this).parent().remove();
	});
	
	$('.dropdown-wrapper').children().first().click(function(e) {
		e.preventDefault();
		$('.cart-dropdown').toggle();
	})	
	
});

	
	
	
	