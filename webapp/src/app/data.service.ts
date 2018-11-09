import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {SResult} from './sresult/SResult';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor() {
  }

  MOCK_SRESULTS: SResult[] = [
    {title: 'title', text: 'text one', score: 54, tags: ['a', 'b']},
    {title: 'Cats', text: 'Cats are nice', score: 44, tags: ['a']},
    {title: 'Dogs', text: 'I don\'t like dogs', score: 38, tags: ['a', 'b']},
    {title: 'Rain', text: 'Cats and dogs', score: 20, tags: ['b']}
  ];

  getData(query: String): Observable<SResult[]> {
    return of(this.MOCK_SRESULTS);
  }
}
