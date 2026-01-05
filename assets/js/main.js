$(function () {

    // Loading Screen with Cookie Control
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    function initLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        const lottieContainer = document.getElementById('lottie-container');
        
        // Cookie kontrolü
        const loadingShown = getCookie('loadingShown');
        
        if (loadingShown === 'true') {
            // Cookie varsa loading'i gösterme
            if (loadingScreen) {
                loadingScreen.classList.add('hidden');
            }
            return;
        }

        // Cookie yoksa loading'i göster ve animasyonu başlat
        if (loadingScreen && lottieContainer) {
            loadingScreen.classList.remove('hidden');
            
            // Lottie animasyonunu yükle
            const animation = lottie.loadAnimation({
                container: lottieContainer,
                renderer: 'svg',
                loop: false,
                autoplay: true,
                path: 'images/loading.json'
            });

            // Animasyon bittiğinde fade out yap
            animation.addEventListener('complete', function() {
                loadingScreen.classList.add('fade-out');
                
                // Fade out tamamlandıktan sonra gizle
                setTimeout(function() {
                    loadingScreen.classList.add('hidden');
                    // Cookie'yi 1 gün için ayarla
                    setCookie('loadingShown', 'true', 1);
                }, 500);
            });
        }
    }

    // Sayfa yüklendiğinde loading'i başlat
    if (document.readyState === 'loading') {
        // document.addEventListener('DOMContentLoaded', initLoadingScreen);
    } else {
        //initLoadingScreen();
    }

    $(document).ready(function($) {
        let lastScrollTop = 0;
        const headerTop = $('.header-top');
        const isDesktop = () => window.innerWidth > 992;

        $(window).scroll(function () {
            const scrollTop = $(this).scrollTop();
            
            // Logo ve header scroll kontrolü
            if (scrollTop > 40) {
                $('.logo img').addClass('small-logo');
                $('header').addClass('scrolled');
            } else {
                $('.logo img').removeClass('small-logo');
                $('header').removeClass('scrolled');
            }

            // Header-top scroll kontrolü (sadece desktop)
            if (isDesktop() && headerTop.length) {
                if (scrollTop > 50) {
                    // Scroll edildiğinde gizle
                    headerTop.addClass('header-top-hidden');
                } else {
                    // En üste çıkıldığında göster
                    headerTop.removeClass('header-top-hidden');
                }
            }
            
            lastScrollTop = scrollTop;
        });

        // Window resize'da kontrol et
        $(window).resize(function() {
            if (!isDesktop()) {
                // Mobile'da header-top zaten display: none, class'ı kaldır
                headerTop.removeClass('header-top-hidden');
            }
        });
    });

    $('.menu-trigger').on('click', function () {
        $(this).toggleClass('active');
        $('.menu').toggleClass('active');
        $('body').toggleClass('hidden');
        $(window).scrollTop(0);
        return false;
    });

    $('.menu li .sub-menu').parent().append('<span class="sub-down"><i class="fa fa-angle-down"></i></span>');
    $('.sub-down').parent().find('a').on('click', function () {
        $(this).toggleClass('active');
        $(this).parent().find('.sub-menu').toggle();
    });



    // Theme toggle switch elementleri
    const themeSwitch = document.getElementById('check');
    const themeSwitchMobile = document.getElementById('check-mobile');

    // Sayfa yüklendiğinde localStorage'dan tema durumunu al
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Eğer dark theme aktifse checkbox'ları işaretle
    if (currentTheme === 'dark') {
      if (themeSwitch) themeSwitch.checked = true;
      if (themeSwitchMobile) themeSwitchMobile.checked = true;
    }

    // Tema değiştirme fonksiyonu
    const changeTheme = (isDark) => {
      if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
      }
      // Her iki checkbox'ı senkronize tut
      if (themeSwitch) themeSwitch.checked = isDark;
      if (themeSwitchMobile) themeSwitchMobile.checked = isDark;
    };

    // Desktop toggle değiştiğinde tema değiştir
    if (themeSwitch) {
      themeSwitch.addEventListener('change', () => {
        changeTheme(themeSwitch.checked);
      });
    }

    // Mobil toggle değiştiğinde tema değiştir
    if (themeSwitchMobile) {
      themeSwitchMobile.addEventListener('change', () => {
        changeTheme(themeSwitchMobile.checked);
      });
    }





});