FROM php:7.2-fpm

#
#--------------------------------------------------------------------------
# Software's Installation
#--------------------------------------------------------------------------
#
# Installing tools and PHP extentions using "apt", "docker-php", "pecl",
#

# Install "curl", "libmemcached-dev", "libpq-dev", "libjpeg-dev",
#         "libpng-dev", "libfreetype6-dev", "libssl-dev", "libmcrypt-dev",
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    curl unzip git zip \
    libmemcached-dev \
    libz-dev \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libssl-dev \
    libmcrypt-dev \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update -yqq && \
    apt-get install -y apt-utils && \
    pecl channel-update pecl.php.net


  # Install the PHP pdo_mysql extention
RUN docker-php-ext-install pdo_mysql \
  # Install the PHP pdo_pgsql extention
  && docker-php-ext-install pdo_pgsql \
  # Install the PHP gd library
  && docker-php-ext-configure gd \
    --enable-gd-native-ttf \
    --with-jpeg-dir=/usr/lib \
    --with-freetype-dir=/usr/include/freetype2 && \
  docker-php-ext-install gd


RUN docker-php-ext-install zip
RUN docker-php-ext-install pgsql
RUN docker-php-ext-install mbstring
RUN docker-php-ext-install fileinfo

RUN chown -R www-data:www-data /var/www

WORKDIR /root
RUN curl --silent --show-error https://getcomposer.org/installer | php
RUN ln -s ~/composer.phar /usr/bin/composer
RUN chmod +x ~/composer.phar

COPY ./config/php.ini /usr/local/etc/php/

# INSTALL NODEJS NPM BOWER GULP 
RUN apt-get install -y gnupg 
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs && \
    npm install -g npm && \
    npm install -g bower && \
    npm install -g gulp

COPY ./laravel /var/www

WORKDIR /var/www
RUN composer install && composer update
RUN npm install
RUN npm build
RUN npm run dev
RUN cp .env.example .env
RUN php artisan key:generate
RUN php artisan config:cache
RUN php artisan view:clear
#RUN php artisan migrate
#RUN php artisan db:seed