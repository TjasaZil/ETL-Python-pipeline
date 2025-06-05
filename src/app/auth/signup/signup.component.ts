import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [MaterialModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.scss',
})
export class SignupComponent {}
