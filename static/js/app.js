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

        // set up router and let it take over
        var appRouter = new Router();
        
        Backbone.history.start();

        // if (!me.id) then they're not logged in
        if (!me.id) {
            appRouter.navigate('start', {trigger: true});
        } else {
            appRouter.navigate('home', {trigger: true});
        }
    });
});
