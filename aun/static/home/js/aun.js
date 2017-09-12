app = new Vue({
    el: "#app",
    data: {
        currentView: "",
        news: [], // 新闻列表
        slideShows: [], // 轮播图
        post: {}, // 当前新闻
        clubs: [], // 社团列表
        club: {}, // 当前社团
        assets: [],
        NEWS: {
            timeFilter: 1 / 0,
            typeFilter: "",
        },
        CLUBS: {
            typeFilter: "",
        },
        ABOUT: {
            tabs: ["财务部", "社联外联企划部", "秘书部", "人力资源部", "社团部", "行政监察部", "外联部", "公共关系部", "媒体部", "宣传部", "思存工作室", "新媒体工作室", "文艺拓展部"],
            tab: "",
        }
    },
    methods: {
        getSlideShows: function () {
            return ($.ajax({
                url: "/api/news/slideshow",
                dataType: "text",
            }).done(function (data) {
                app.slideShows = JSON.parse(data);
            }))
        },
        getNews: function () { // 取得所有新闻列表
            return ($.ajax({
                url: "/api/news/news",
                dataType: "text",
            }).done(function (data) {
                app.news = JSON.parse(data);
            }));
        },
        getPost: function (postId) { // 取得具体一篇新闻
            return ($.ajax({
                url: "/api/news/news/" + postId,
                dataType: "text",
            }).done(function (data) {
                app.post = JSON.parse(data);
            }));
        },
        getClubs: function () {
            return ($.ajax({
                url: "/api/clubs",
                dataType: "text",
            }).done(function (data) {
                app.clubs = JSON.parse(data);
            }))
        },
        getAssets: function () {
            return ($.ajax({
                url: "/api/data-station?status=2&is_important=2",
                dataType: "text",
            }).done(function (data) {
                app.assets = JSON.parse(data);
            }));
        },
        getRandomFrom: function (seq, num) {
            var shuffled = seq.slice(0);
            var i = seq.length;
            var min = i - num;
            var temp, index;
            while(i-- > min) {
                index = Math.floor((i + 1) * Math.random());
                temp = shuffled[index];
                shuffled[index] = shuffled[i];
                shuffled[i] = temp;
            }
            return shuffled.slice(min);
        },
    }
});

page("/", function (ctx, next) { // 首页
    app.getNews().done(function () {
        app.getSlideShows().done(function () {
            app.currentView = "home";
            // return;
            Vue.nextTick(function () {
                $('#carousel').slick({
                    dots: true,
                    infinite: true,
                    speed: 500,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000
                });
            });
            app.getAssets();
        });
    });
    app.getClubs();
});

page("/news", function (ctx, next) { // 新闻
    app.getNews().always(function () {
        app.currentView = "news";
    });
});

page("/news/:postId", function (ctx, next) { // 具体新闻
    app.getPost(ctx.params.postId).always(function () {
        app.currentView = "news-post";
    });
});

page("/association/@:clubName", function (ctx, next) { // 社团空间
    app.getNews();
    app.getClubs().always(function () {
        app.currentView = "clubs-club";
    }).done(function () {
        app.club = app.clubs.filter(function (i) {
            if (i.name === ctx.params.clubName) {
                return (true);
            } else {
                return (false);
            }
        })[0];
        $.ajax({
            url: "/api/clubs/" + app.club.id + "/articles",
            dataType: "text",
        }).done(function(data) {
            app.news = JSON.parse(data);
        });
    })
    // app.getClub(ctx.params.club.id).always(function() {
    // 	app.currentView = "clubs-club";
    //
    // })
});

page("/clubs", function (ctx, next) { // 所有社团
    app.getClubs().always(function () {
        app.currentView = "clubs";
    });
});

page("/about", function (ctx, next) { // 社联介绍
    app.currentView = "about";
    app.ABOUT.tab = "";
});

page("/about/:sec", function (ctx, next) { // 社联介绍
    app.currentView = "about";
    app.ABOUT.tab = ctx.params.sec;
});

page("/assets", function (ctx, next) { // 资料站
    app.getAssets().always(function () {
        app.currentView = "assets";
    });
});

page("/signup", function (ctx, next) { // 报名
    app.currentView = "signup";
});

page("*", function (ctx, next) { // 404
    if (app.currentView === "") { // 地址栏url错误

    } else { // 页面上url错误

    }
});

$(document).ready(function () {
    page.start();
});
