import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
@Component({
  selector: 'app-welcome-view',
  standalone: true,
  imports: [MaterialModule],
  templateUrl: './welcome-view.component.html',
  styleUrl: './welcome-view.component.scss',
})
export class WelcomeViewComponent {}
