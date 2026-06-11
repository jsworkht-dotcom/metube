import { TestBed } from '@angular/core/testing';
import { HttpClient } from '@angular/common/http';
import { Subject, of } from 'rxjs';
import { App } from './app';
import { type Download } from './interfaces';
import { DownloadsService } from './services/downloads.service';
import { SubscriptionsService } from './services/subscriptions.service';
import { CookieService } from 'ngx-cookie-service';

class DownloadsServiceStub {
  loading = false;
  queue = new Map();
  done = new Map();
  configuration: Record<string, unknown> = { CUSTOM_DIRS: true, CREATE_CUSTOM_DIRS: true, ALLOW_YTDL_OPTIONS_OVERRIDES: false };
  customDirs = { download_dir: [], audio_download_dir: [] };
  queueChanged = new Subject<void>();
  doneChanged = new Subject<void>();
  configurationChanged = new Subject<Record<string, unknown>>();
  customDirsChanged = new Subject<Record<string, string[]>>();
  ytdlOptionsChanged = new Subject<Record<string, unknown>>();
  updated = new Subject<void>();

  getCookieStatus() {
    return of({ status: 'ok', has_cookies: false });
  }

  getPresets() {
    return of({ presets: ['Preset A'] });
  }

  add() {
    return of({ status: 'ok' as const });
  }

  cancelAdd() {
    return of({ status: 'ok' as const });
  }

  startById() {
    return of({});
  }

  delById() {
    return of({});
  }

  delByFilter() {
    return of({});
  }

  startByFilter() {
    return of({});
  }

  uploadCookies() {
    return of({ status: 'ok' });
  }

  deleteCookies() {
    return of({ status: 'ok' });
  }
}

class SubscriptionsServiceStub {
  subscriptions = new Map();
  subscriptionsChanged = new Subject<void>();
  subscribeCalls: unknown[] = [];

  subscribe(payload: unknown) {
    this.subscribeCalls.push(payload);
    return of({ status: 'ok' as const });
  }

  delete() {
    return of({});
  }

  update() {
    return of({ status: 'ok' as const });
  }

  refreshList() {
    return of([]);
  }
}

class CookieServiceStub {
  private cookies = new Map<string, string>();

  get(name: string) {
    return this.cookies.get(name) ?? '';
  }

  set(name: string, value: string) {
    this.cookies.set(name, value);
  }

  check(name: string) {
    return this.cookies.has(name);
  }
}

interface HttpClientMock {
  get: ReturnType<typeof vi.fn>;
}

const buildDownload = (overrides: Partial<Download>): Download => ({
  id: 'test-id',
  title: 'Test download',
  url: 'https://example.com/watch?v=test',
  download_type: 'video',
  quality: 'best',
  format: 'mp4',
  folder: '',
  custom_name_prefix: '',
  playlist_item_limit: 0,
  status: 'finished',
  msg: '',
  percent: 100,
  speed: 0,
  eta: 0,
  filename: 'test.mp4',
  checked: false,
  ...overrides,
});

describe('App', () => {
  let downloads: DownloadsServiceStub;

  beforeEach(async () => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      enumerable: true,
      value: vi.fn().mockImplementation((query: string) => ({
        matches: false,
        media: query,
        onchange: null,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    });
    downloads = new DownloadsServiceStub();
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        { provide: DownloadsService, useValue: downloads },
        { provide: SubscriptionsService, useClass: SubscriptionsServiceStub },
        { provide: CookieService, useClass: CookieServiceStub },
        {
          provide: HttpClient,
          useValue: {
            get: vi.fn().mockReturnValue(of({ 'yt-dlp': 'test', version: 'test' })),
          },
        },
      ],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('shows development update status for dev builds', () => {
    const http = TestBed.inject(HttpClient) as unknown as HttpClientMock;
    http.get.mockImplementation((url: string) => {
      if (url.endsWith('version')) {
        return of({ 'yt-dlp': '2026.03.17', version: 'dev' });
      }
      if (url.endsWith('update-status')) {
        return of({ status: 'development' });
      }
      return of({});
    });

    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    fixture.detectChanges();

    const app = fixture.componentInstance;
    const root = fixture.nativeElement as HTMLElement;
    expect(app.updateStatusKind).toBe('development');
    expect(app.updateStatusLabel).toBe('開発版');
    expect(root.textContent).toContain('開発版');
  });

  it('hides manual override input when disabled', () => {
    const fixture = TestBed.createComponent(App);
    fixture.componentInstance.isAdvancedOpen = true;
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('input[name="ytdlOptionsOverrides"]')).toBeNull();

    const presetWrapper = root.querySelector('ng-select[name="ytdlOptionsPresets"]')?.closest('.col-12');
    expect(presetWrapper?.classList.contains('col-md-6')).toBe(false);

    const presetRow = root.querySelector('ng-select[name="ytdlOptionsPresets"]')?.closest('.row');
    expect(presetRow?.querySelector('input[name="checkIntervalMinutes"]')).toBeNull();
  });

  it('shows manual override input when enabled', () => {
    downloads.configuration['ALLOW_YTDL_OPTIONS_OVERRIDES'] = true;

    const fixture = TestBed.createComponent(App);
    fixture.componentInstance.isAdvancedOpen = true;
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('input[name="ytdlOptionsOverrides"]')).not.toBeNull();

    const presetWrapper = root.querySelector('ng-select[name="ytdlOptionsPresets"]')?.closest('.col-12');
    expect(presetWrapper?.classList.contains('col-md-6')).toBe(true);

    const presetRow = root.querySelector('ng-select[name="ytdlOptionsPresets"]')?.closest('.row');
    expect(presetRow?.querySelector('input[name="checkIntervalMinutes"]')).toBeNull();
    expect(presetRow?.querySelector('input[name="ytdlOptionsOverrides"]')).not.toBeNull();
  });

  it('does not submit manual overrides when disabled', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    app.ytdlOptionsOverrides = '{"exec":"echo hi"}';

    const payload = app['buildAddPayload']();

    expect(payload.ytdlOptionsOverrides).toBe('');
  });

  it('includes titleRegex in subscribe payload', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const subs = TestBed.inject(SubscriptionsService) as unknown as SubscriptionsServiceStub;
    app.addUrl = 'https://example.com/channel';
    app.titleRegex = 'EPISODE';
    app.addSubscription();
    expect(subs.subscribeCalls.length).toBe(1);
    const payload = subs.subscribeCalls[0] as { titleRegex: string; skipSubscriberOnly: boolean };
    expect(payload.titleRegex).toBe('EPISODE');
    expect(payload.skipSubscriberOnly).toBe(false);
  });

  it('includes skipSubscriberOnly true when checked', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const subs = TestBed.inject(SubscriptionsService) as unknown as SubscriptionsServiceStub;
    app.addUrl = 'https://example.com/channel';
    app.skipSubscriberOnly = true;
    app.addSubscription();
    expect(subs.subscribeCalls.length).toBe(1);
    const payload = subs.subscribeCalls[0] as { skipSubscriberOnly: boolean };
    expect(payload.skipSubscriberOnly).toBe(true);
  });

  it('omits clip fields from subscribe payload', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const subs = TestBed.inject(SubscriptionsService) as unknown as SubscriptionsServiceStub;
    app.addUrl = 'https://example.com/channel';
    app.clipStart = '1:00';
    app.clipEnd = '2:00';
    app.addSubscription();
    expect(subs.subscribeCalls.length).toBe(1);
    const payload = subs.subscribeCalls[0] as Record<string, unknown>;
    expect('clipStart' in payload).toBe(false);
    expect('clipEnd' in payload).toBe(false);
  });

  it('formats completed video quality labels with selector wording', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const labels = ['best', 'worst', '2160', '1440', '1080', '720', '480', '360', '240', '999'].map(
      quality => app.formatQualityLabel(buildDownload({ download_type: 'video', quality })),
    );

    expect(labels).toEqual([
      '最高画質（自動）',
      '最低画質（自動）',
      '4K（2160p）',
      '高画質（1440p）',
      'フルHD（1080p）',
      '標準（720p）',
      '軽量（480p）',
      '低容量（360p）',
      '最小（240p）',
      '999p',
    ]);
  });

  it('formats completed audio quality labels with selector wording', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const labels = ['best', '320', '192', '128', '256'].map(quality =>
      app.formatQualityLabel(buildDownload({ download_type: 'audio', quality })),
    );

    expect(labels).toEqual([
      '最高音質（自動）',
      '高音質（320kbps）',
      '標準（192kbps）',
      '軽量（128kbps）',
      '256kbps',
    ]);
  });

  it('keeps caption and thumbnail result quality labels hidden', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    expect(app.formatQualityLabel(buildDownload({ download_type: 'captions', quality: 'best' }))).toBe(
      '-',
    );
    expect(app.formatQualityLabel(buildDownload({ download_type: 'thumbnail', quality: 'best' }))).toBe(
      '-',
    );
  });

  it('keeps a safe fallback for unknown result quality labels', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    expect(app.formatQualityLabel(buildDownload({ download_type: 'video', quality: 'custom' }))).toBe(
      'Custom',
    );
    expect(app.formatQualityLabel(buildDownload({ download_type: 'audio', quality: 'lossless' }))).toBe(
      'Lossless',
    );
  });

  it('buildAddPayload includes clip times', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    app.clipStart = '0:10';
    app.clipEnd = '1:20';
    const payload = app['buildAddPayload']();
    expect(payload.clipStart).toBe('0:10');
    expect(payload.clipEnd).toBe('1:20');
  });

  it('blocks subscribe with invalid title regex', () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => undefined);
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const subs = TestBed.inject(SubscriptionsService) as unknown as SubscriptionsServiceStub;
    app.addUrl = 'https://example.com/channel';
    app.titleRegex = '[';
    app.addSubscription();
    expect(subs.subscribeCalls.length).toBe(0);
    expect(alertSpy).toHaveBeenCalledWith('Invalid subscription title filter (regex)');
    alertSpy.mockRestore();
  });
});
