import { Component, OnInit } from '@angular/core';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  testObj : any

  constructor(private _mainService:MainService) { }

  ngOnInit(): void {
    this._mainService.getData().subscribe(data => this.testObj = data)
  }
}
