import React from 'react';
import { Route, Switch } from 'react-router-dom';

import { Overview } from './Overview';
import { Users } from './users';
import { Categories } from './categories';

function Admin({ match }) {
    const { path } = match;

    return (
        <div className="pt30">
            <div className="container">
                <Switch>
                    <Route exact path={path} component={Overview} />
                    <Route path={`${path}/users`} component={Users} />
                    <Route path={`${path}/categories`} component={Categories} />
                </Switch>
            </div>
        </div>
    );
}

export { Admin };