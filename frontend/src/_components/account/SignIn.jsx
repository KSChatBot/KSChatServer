import React from 'react';
import { Link } from 'react-router-dom';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';

import { accountService, alertService } from '@/_services';

function SignIn({ isOpen, close, openSignupModal }) {
    const initialValues = {
        email: '',
        password: ''
    };

    const validationSchema = Yup.object().shape({
        email: Yup.string()
            .email('Email is invalid')
            .required('Email is required'),
        password: Yup.string().required('Password is required')
    });

    function onSubmit({ email, password }, { setSubmitting }) {
        alertService.clear();
        accountService.login(email, password)
            .then(() => {
                close();
            })
            .catch(error => {
                setSubmitting(false);
                alertService.error(error);
            });
    }

    const openSignup = () => {
        close();
        openSignupModal();
    }

    return (
        <>
            {isOpen? (
                <div id="login" role="dialog">
                    <div className="modal fade show" onClick={close}></div>
                    <div className="modal-dialog modal-dialog-centered login-pop-form" role="document">
                        <div className="modal-content" id="registermodal">
                            <span className="mod-close"><i className="fas fa-times" onClick={close}></i></span>
                            <div className="modal-body">
                                <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
                                    {({ errors, touched, isSubmitting }) => (
                                        <Form>
                                            <h3 className="card-header">Login</h3>
                                            <div className="card-body">
                                                <div className="form-group">
                                                    <label>Email</label>
                                                    <Field name="email" type="text" className={'form-control' + (errors.email && touched.email ? ' is-invalid' : '')} />
                                                    <ErrorMessage name="email" component="div" className="invalid-feedback" />
                                                </div>
                                                <div className="form-group">
                                                    <label>Password</label>
                                                    <Field name="password" type="password" className={'form-control' + (errors.password && touched.password ? ' is-invalid' : '')} />
                                                    <ErrorMessage name="password" component="div" className="invalid-feedback" />
                                                </div>
                                                <div className="form-row">
                                                    <div className="form-group col">
                                                        <button type="submit" disabled={isSubmitting} className="btn btn-primary">
                                                            {isSubmitting && <span className="spinner-border spinner-border-sm mr-1"></span>}
                                                            Login
                                                        </button>
                                                        {/*<a className="btn btn-link" onClick={openSignup}>Register</a>*/}
                                                    </div>
                                                    <div className="form-group col text-right">
                                                        <Link to="forgot-password" className="btn btn-link pr-0">Forgot Password?</Link>
                                                    </div>
                                                </div>
                                            </div>
                                        </Form>
                                    )}
                                </Formik>
                            </div>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    )
}

export { SignIn }; 