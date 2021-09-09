$(function(){
  var topBtn=$('#pageTop');
  var menuBtn=$('.navbar-toggler');
  topBtn.hide();

  $(window).scroll(function(){
    if($(this).scrollTop()>500){
      topBtn.fadeIn();
    }else{
      topBtn.fadeOut();
    }
  });

  topBtn.click(function(){
    $('body,html').animate({
      scrollTop: 0},500);
    return false;
  });


if (0) {
  var header = $('header', top.frames[0].document.body).html();
  console.log(header);
  $('#mainheader').html(header);
  var menu = $('#sidemenu', top.frames[1].document.body).html();
  $('#mainsidemenu').html(menu);
  var footer = $('footer', top.frames[3].document.body).html();
  $('#mainfooter').html(footer);
}

  var menu_default_close = function(){
    $('.navbar-nav .nav-item.lv1.close').nextUntil('.nav-item.lv1','.nav-item.lv2.close').hide();
    $('.navbar-nav .nav-item.lv2.close').nextUntil('.nav-item.lv2','.nav-item.lv3.close').hide();
    $('.navbar-nav .nav-item.lv3.close').nextUntil('.nav-item.lv3','.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').hide();
  }

  var menu_open = function(that){
    if ($(that).parents('.close').hasClass('lv1')) {
      // lv2を全て開く
      $(that).parents('.close').nextUntil('.nav-item.lv1','.nav-item.lv2').show();
      // lv2.openのlv3を開く
      $(that).parents('.close').nextUntil('.nav-item.lv1','.nav-item.lv2.open').nextUntil('.nav-item.lv2','.nav-item.lv3').show();
      // lv3.openのlv4/5/6/7を開く
      $(that).parents('.close').nextUntil('.nav-item.lv1','.nav-item.lv2.open').nextUntil('.nav-item.lv2','.nav-item.lv3.open').nextUntil('.nav-item.lv3','.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').show();
    }
    if ($(that).parents('.close').hasClass('lv2')) {
      // lv3を全て開く
      $(that).parents('.close').nextUntil('.nav-item.lv2','.nav-item.lv3').show();
      // lv3.openのlv4/5/6/7を開く
      $(that).parents('.close').nextUntil('.nav-item.lv2','.nav-item.lv3.open').nextUntil('.nav-item.lv3','.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').show();
    }
    if ($(that).parents('.close').hasClass('lv3')) {
      $(that).parents('.close').nextUntil('.nav-item.lv3','.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').show();
    }
    // class
    $(that).parents('.close').removeClass('close').addClass('open');

  }

  var menu_close = function(that){
    if ($(that).parents('.open').hasClass('lv1')) {
      $(that).parents('.open').nextUntil('.nav-item.lv1','.nav-item.lv2,.nav-item.lv3,.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').hide();
    }
    if ($(that).parents('.open').hasClass('lv2')) {
      $(that).parents('.open').nextUntil('.nav-item.lv2','.nav-item.lv3,.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').hide();
    }
    if ($(that).parents('.open').hasClass('lv3')) {
      $(that).parents('.open').nextUntil('.nav-item.lv3','.nav-item.lv4,.nav-item.lv5,.nav-item.lv6,.nav-item.lv7').hide();
    }
    // class
    $(that).parents('.open').removeClass('open').addClass('close');
  }

  menu_default_close();

  $(document).on('click', '.navbar-nav .nav-item.close .icon-link', function(){
    menu_open(this);
    return false;
  });
  
  $(document).on('click', '.navbar-nav .nav-item.open .icon-link', function(){
    menu_close(this);
    return false;
  });

  $('.inacrive').on('click', function(){
    return false;
  });

  if (window.matchMedia('(min-width:992px)').matches) {
    $('body.slide .drawer-hamburger').on('click.one', function(){
      $('.drawer').drawer('toggle');
    });
  }

  $(document).on('keydown', function(e) {
    console.log(e.originalEvent.keyCode);
    switch (e.originalEvent.keyCode) {
    case 37:
      // Key: 
      $("#btn_prev.active span").click();
      break;
    case 39:
      // Key: 
      $("#btn_next.active span").click();
      break;
    }
    
  });


  // ==============================================
  // スライド高さ設定
  if ($('body').hasClass('slide')) {
    var setSlideHeight = function(){
      var winh = $(window).height();
      if (window.matchMedia('(min-width:992px)').matches) {
        $('.content').height(winh - 280);
      } else {
        $('.content').height(winh - 200);
      }
    };
    $(window).on('resize', function() {
      setSlideHeight();
    });
    setSlideHeight();
  }


  // ==============================================
  // スライドフリック動作

  // 移動する要素の親要素(スワイプ後の位置を確認するのに使用)
  var swWrap = $('.slide section');
  // 移動する要素
  var sw = swWrap.children('.content');
  var isTouch = ('ontouchstart' in window);

  // 初期位置
  var basePoint;
  // 移動する要素にイベントが発生した時
  sw.bind({
    // タッチ開始
    'touchstart mousedown': function(e) {
      e.preventDefault();
      var event = e;
      // 画面の左端からの座標
      basePoint = (isTouch ? event.changedTouches[0].pageX : e.pageX);
      this.touched = true;
    },
    // タッチ終了
    'touchend mouseup': function(e) {
      if(!this.touched) {
        return;
      }
      this.touched = false;
      var event = e;
      basePoint2 = (isTouch ? event.changedTouches[0].pageX : e.pageX);

      // 移動要素が親要素の範囲より右にはみ出しているとき
      if(basePoint - basePoint2 > 0) {
        $("#btn_next.active span").click();

      // 移動要素が親要素の範囲より左にはみ出しているとき
      } else if(basePoint - basePoint2 < 0) {
        $("#btn_prev.active span").click();
      } else {
      }
    }
  });


});
