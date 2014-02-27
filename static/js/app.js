define(function(require){
    'use strict';

    requirejs.config({
        enforceDefine: true,
        inlineText: true,
        urlArgs: "bust=" + (new Date()).getTime()
    });

    var Router = require('Router'),
        User   = require('models/User');

    var me = new User();
    me.fetch().complete(function() {

        // create router/views
        var appRouter = new Router();
        
        Backbone.history.start();

        if (!me.id) {
            appRouter.navigate('start', {trigger: true});
        } else {
            appRouter.navigate('home', {trigger: true});
        }
    });
});
