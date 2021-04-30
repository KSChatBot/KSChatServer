import React, { useState, useEffect } from 'react';
import { NavLink, Route } from 'react-router-dom';

import { Role } from '@/_helpers';
import { accountService } from '@/_services';

import { SignIn, SignUp } from '@/_components';

function Nav() {
    const [user, setUser] = useState({});
    const [signinModalOpen, setSigninModalOpen] = useState(false);
    const [signupModalOpen, setSignupModalOpen] = useState(false);
    const [scrollTop, setScrollTop] = useState(0);

    const openSigninModal = () => {
        setSigninModalOpen(true);
    };

    const closeSigninModal = () => {
        setSigninModalOpen(false);
    }

    const openSignupmodal = () => {
        setSignupModalOpen(true);
    }

    const closeSignupModal = () => {
        setSignupModalOpen(false);
    }

    useEffect(() => {
        const subscription = accountService.user.subscribe(x => setUser(x));
        window.addEventListener('scroll', (e) => {
            const scrollTop = e.target.scrollingElement.scrollTop;
            setScrollTop(scrollTop);
        });
        return subscription.unsubscribe;
    }, []);

    // only show nav when logged in

    return (
        <div id="header" className={"header " + (window.location.pathname === '/'? 'dark-theme ' : 'light-theme ') + (scrollTop > 20? 'fixed' : '')}>
            <div className="container">
                <nav id="navigation" className="navigation">
                    <div className="nav-header">
                        {window.location.pathname === '/' && scrollTop <= 20 ? (
                            <NavLink exact to="/" className="nav-brand dark-theme-logo">
                                <img src="/images/2020_KS_NEWLOGO_LOGOTYPE_b&amp;w_02.png" />
                            </NavLink>
                        ) : (
                            <NavLink exact to="/" className="nav-brand light-theme-logo">
                                <img src="/images/2020_KS_NEWLOGO_LOGOTYPE_b&amp;w_01.png" />
                            </NavLink>
                        )}
                    </div>
                    <div className="nav-menus-wrapper">
                        {user && 
                            <ul className="nav-menu">
                                {user.role === Role.Admin &&
                                    <li className=""><NavLink to="/admin" className="nav-item nav-link">시스템 관리</NavLink></li>
                                }
                                <li className=""><NavLink exact to="/api" className="">컨텐츠 관리</NavLink></li>
                            </ul>
                        }
                        {!user &&
                            <ul className="nav-menu align-to-right">
                                <li className="login_click bg-red"><a onClick={openSigninModal}>Sign in</a></li>
                                {/*<li className="login_click bg-blue"><a onClick={openSignupmodal}>Sign up</a></li>*/}
                            </ul>
                        }
                        {user && 
                            <ul className="nav-menu align-to-right">
                                <li className=""><NavLink exact to="/profile" className="">사용자 정보</NavLink></li>
                                <li><a onClick={accountService.logout} className="">로그아웃</a></li>
                            </ul>
                        }
                    </div>
                </nav>
                <Route path="/admin" component={AdminNav} />
            </div>
            <SignIn isOpen={signinModalOpen} close={closeSigninModal} openSignupModal={openSignupmodal} />
            <SignUp isOpen={signupModalOpen} close={closeSignupModal} />
        </div>
    );

    /*if (!user) return null;

    return (
        <div>
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <div className="navbar-nav">
                    <NavLink exact to="/" className="nav-item nav-link">Home</NavLink>
                    <NavLink to="/profile" className="nav-item nav-link">Profile</NavLink>
                    {user.role === Role.Admin &&
                        <NavLink to="/admin" className="nav-item nav-link">Admin</NavLink>
                    }
                    <NavLink to="/api" className="nav-item nav-link">Api</NavLink>
                    <a onClick={accountService.logout} className="nav-item nav-link">Logout</a>
                </div>
            </nav>
            <Route path="/admin" component={AdminNav} />
        </div>
    );*/
}

function AdminNav({ match }) {
    const { path } = match;

    return (
        <nav className="admin-nav navbar navbar-expand navbar-light">
            <div className="navbar-nav">
                <NavLink to={`${path}/users`} className="nav-item nav-link">Users</NavLink>
                <NavLink to={`${path}/categories`} className="nav-item nav-link">Categories</NavLink>
            </div>
        </nav>
    );
}

export { Nav }; 