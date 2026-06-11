import { Quality } from "./quality";

export interface Option {
  id: string;
  text: string;
}

export interface AudioFormatOption extends Option {
  qualities: Quality[];
}

export const DOWNLOAD_TYPES: Option[] = [
  { id: "video", text: "動画" },
  { id: "audio", text: "音声" },
  { id: "captions", text: "字幕" },
  { id: "thumbnail", text: "サムネイル" },
];

export const VIDEO_CODECS: Option[] = [
  { id: "auto", text: "自動" },
  { id: "h264", text: "H.264" },
  { id: "h265", text: "H.265 (HEVC)" },
  { id: "av1", text: "AV1" },
  { id: "vp9", text: "VP9" },
];

export const VIDEO_FORMATS: Option[] = [
  { id: "any", text: "自動" },
  { id: "mp4", text: "MP4" },
  { id: "ios", text: "iOS向け" },
];

export const VIDEO_QUALITIES: Quality[] = [
  { id: "best", text: "最高画質（自動）" },
  { id: "2160", text: "4K（2160p）" },
  { id: "1440", text: "高画質（1440p）" },
  { id: "1080", text: "フルHD（1080p）" },
  { id: "720", text: "標準（720p）" },
  { id: "480", text: "軽量（480p）" },
  { id: "360", text: "低容量（360p）" },
  { id: "240", text: "最小（240p）" },
  { id: "worst", text: "最低画質（自動）" },
];

export const AUDIO_FORMATS: AudioFormatOption[] = [
  {
    id: "m4a",
    text: "M4A",
    qualities: [
      { id: "best", text: "最高音質（自動）" },
      { id: "192", text: "標準（192kbps）" },
      { id: "128", text: "軽量（128kbps）" },
    ],
  },
  {
    id: "mp3",
    text: "MP3",
    qualities: [
      { id: "best", text: "最高音質（自動）" },
      { id: "320", text: "高音質（320kbps）" },
      { id: "192", text: "標準（192kbps）" },
      { id: "128", text: "軽量（128kbps）" },
    ],
  },
  { id: "opus", text: "OPUS", qualities: [{ id: "best", text: "最高音質（自動）" }] },
  { id: "wav", text: "WAV", qualities: [{ id: "best", text: "最高音質（自動）" }] },
  { id: "flac", text: "FLAC", qualities: [{ id: "best", text: "最高音質（自動）" }] },
];

export const CAPTION_FORMATS: Option[] = [
  { id: "srt", text: "SRT" },
  { id: "txt", text: "TXT (テキストのみ)" },
  { id: "vtt", text: "VTT" },
  { id: "ttml", text: "TTML" },
];

export const THUMBNAIL_FORMATS: Option[] = [{ id: "jpg", text: "JPG" }];
