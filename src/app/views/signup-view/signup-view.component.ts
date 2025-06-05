import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';

@Component({
  selector: 'app-signup-view',
  standalone: true,
  imports: [MaterialModule],
  templateUrl: './signup-view.component.html',
  styleUrl: './signup-view.component.scss',
})
export class SignupViewComponent {}
