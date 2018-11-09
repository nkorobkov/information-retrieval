import {Component, OnInit, Input} from '@angular/core';
import {SResult} from './SResult';

@Component({
  selector: 'app-sresult',
  templateUrl: './sresult.component.html',
  styleUrls: ['./sresult.component.css']
})
export class SResultComponent implements OnInit {

  @Input() sresult: SResult;
  constructor() {}
  ngOnInit() {
  }

}
