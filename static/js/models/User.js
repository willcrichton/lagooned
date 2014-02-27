define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        urlRoot: '/api/user',
        defaults: {
            name: ''
        }
    });
});
