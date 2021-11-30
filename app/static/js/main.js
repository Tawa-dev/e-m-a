class UI {
    slidesShow() {
    $("#slides").superslides({
      animation: "slide",
      play: 5000,
      pagination: false,
    });
  }
}


eventListeners();
function eventListeners() {
  const ui = new UI();

  //ACTIVATING OUR SLIDES
  $(document).ready(function () {
    ui.slidesShow();
  });
  
}
