import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
@Component({
  selector: 'app-login-view',
  standalone: true,
  imports: [MaterialModule],
  templateUrl: './login-view.component.html',
  styleUrl: './login-view.component.scss',
})
export class LoginViewComponent {}
