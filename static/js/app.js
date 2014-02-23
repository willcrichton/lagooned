define(function(require){
    'use strict';

    requirejs.config({
        enforceDefine: true,
        inlineText: true,
        urlArgs: "bust=" + (new Date()).getTime()
    });

    require(['Router'], function(Router) {

        // create router/views
        var appRouter = new Router();

        Backbone.history.start();
        
        if (!LOGGED_IN) {
            appRouter.navigate('start', {trigger: true});
        } 
    });
});
