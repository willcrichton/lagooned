define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        className: 'User',
        defaults: {
            name: '',
            login: true
        }
    });
});
