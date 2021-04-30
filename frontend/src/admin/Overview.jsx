import React from 'react';
import { Link } from 'react-router-dom';

function Overview({ match }) {
    const { path } = match;

    return (
        <div>
            <h1>시스템 관리</h1>
            <p>This section can only be accessed by administrators.</p>
            <p><Link to={`${path}/users`}>Manage Users</Link></p>
            <p><Link to={`${path}/categories`}>Manage Categories</Link></p>
        </div>
    );
}

export { Overview };