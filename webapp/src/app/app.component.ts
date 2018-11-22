import {Component} from '@angular/core';
import {DataService} from './data.service';
import {SResult} from './sresult/SResult';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'webapp';
  query = '';
  results_ready = false;
  searching = false;
  results: SResult[];

  constructor(private dataService: DataService) {
  }


  getData(): void {
    this.results_ready = false;
    this.searching = true;
    this.dataService.getData(this.query)
      .subscribe(x => {
        this.results = x['hits'].hits;
        console.log(this.results);
        this.results_ready = true;
        this.searching = false;
      });
  }
}
