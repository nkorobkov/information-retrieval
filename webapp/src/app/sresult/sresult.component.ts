import {Component, OnInit, Input} from '@angular/core';
import {SResult} from './SResult';
import {DataService} from '../data.service';


@Component({
  selector: 'app-sresult',
  templateUrl: './sresult.component.html',
  styleUrls: ['./sresult.component.css']
})
export class SResultComponent implements OnInit {

  ner_ready = false;
  ner_searching = false;
  ner_fail = false;
  ner = [];

  @Input() sresult: SResult;


  constructor(private dataService: DataService) {
  }

  ngOnInit() {
  }

  getNER(): void {

    this.ner_searching = true;

    this.dataService.getNER(this.sresult._source.id)
      .subscribe(x => {
        if (x == null){
          this.ner_fail = true;
        }else{
          this.ner = x;
        }
        this.ner_ready = true;
        this.ner_searching = false;
        console.log(x);

      });
  };

}
