import { Routes } from '@angular/router';
import { WelcomeViewComponent } from './views/welcome-view/welcome-view.component';
import { SignupViewComponent } from './views/signup-view/signup-view.component';
import { LoginViewComponent } from './views/login-view/login-view.component';

export const routes: Routes = [
  { path: '', component: WelcomeViewComponent },
  { path: 'signup', component: SignupViewComponent },
  { path: 'login', component: LoginViewComponent },
];
