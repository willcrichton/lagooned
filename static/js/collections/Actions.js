define(function(require) {
    'use strict';

    return Backbone.Collection.extend({
        className: 'Action',
        model: require('models/Action')
    });
});
