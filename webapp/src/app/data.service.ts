import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {SResult} from './sresult/SResult';
import {environment} from '../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';



@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) {
  }

  MOCK_SRESULTS = [
    {title: 'title', annotation: 'text one', score: 54, genre: '', year: 2018, author: 'Nikita'},
    {title: 'Cats', annotation: 'Cats are nice', score: 44, genre: '', year: 2018, author: 'Nikita'},
    {title: 'Dogs', annotation: 'I don\'t like dogs', score: 38, genre: '', year: 2018, author: 'Nikita'},
    {title: 'Rain', annotation: 'Cats and dogs', score: 20, genre: '', year: 2018, author: 'Nikita'}
  ];

  TITLE_SEARCH_DATA = {
    '_source': ['title', 'annotation', 'author', 'genre', 'year'],
    'query': {
      'match': {
        'title': ''
      }
    }
  }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    }),
    method: 'GET'
  };

  // @ts-ignore
  getData(query: string): Observable<> {
    if (environment.mock_api) {
      return of(this.MOCK_SRESULTS);
    }
    return this.queryData(query);
  }

  // @ts-ignore
  queryData(query: string): Observable<> {
    const url = environment.base_url + environment.search_request_template;
    const req_data = this.TITLE_SEARCH_DATA;
    req_data.query.match.title = query;
    return this.http.post<SResult[]>(url, req_data, this.httpOptions);
  }
}
