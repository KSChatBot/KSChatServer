import React from 'react';
import { Route, Switch, Redirect, useLocation } from 'react-router-dom';

import { Role } from '@/_helpers';
import { Nav, PrivateRoute, Alert, Clearfix, Footer } from '@/_components';
import { Home } from '@/home';
import { Profile } from '@/profile';
import { Admin } from '@/admin';
import { Api } from '@/api';

function App() {
    const { pathname } = useLocation();

    return (
        <div className='app-container'>
            <Nav />
            <Clearfix />
            <Alert />
            <Switch>
                <Redirect from="/:url*(/+)" to={pathname.slice(0, -1)} />
                <Route exact path="/" component={Home} />
                <PrivateRoute path="/profile" component={Profile} />
                <PrivateRoute path="/api" component={Api} />
                <PrivateRoute path="/admin" roles={[Role.Admin]} component={Admin} />
                <Redirect from="*" to="/" />
            </Switch>
            {/* credits */}
            <Footer />
        </div>
    );
}

export { App }; 